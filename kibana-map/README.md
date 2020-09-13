# elasticsearch map 기능 사용

## 사전 준비
 * elasitcsearch 서비스 생성
 * public 으로 설정하고
 * 임시적으로 모든 ip 에서 설정이 가능하도록 다음과 같이 엑세스 정책을 수정하였음
 ```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "es:*",
      "Resource": "arn:aws:es:ap-northeast-2:472237031133:domain/dnaoneteam/*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": "0.0.0.0/0"
        }
      }
    }
  ]
}
```
 
 
### index 설정 

* kibana dev 툴에서 인덱스의 mapping (RDBMS 의 스키마와 같은 역할)을 미리 정의함 
```json
PUT dna/
{
    "mappings" : {
      "properties" : {
        "eventtime" : {
          "type" : "date",
          "format": "yyyy-MM-dd HH:mm:ss"
        },
        "country" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "location" : {
          "type" : "geo_point"
        },
        "source_ip" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }, 
        "product" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
}
```

* 정의한 property 는
  - eventtime : 시각 (date type, format 주의)
  - location : 지역에 대한 정보 (lat, lon - 위경도 정보)
  - source_ip : IP 주소
  - product : 상품 정보
  
* type 부가 설명
 - geo_point : 위경도를 의미하며 다음과 같은 형태로 저장함 
 ```json
    "location": { 
        "lat": 37.2979833,
        "lon": 127.071765
    }
```
 - date : 시간값을 의미하며 format 에 따라 달라질 수 있음
 - text : 토큰으로 분해되는 단순 문자열 
 - keyword : 입력값 그대로 인덱싱 됨

* mapping 에 정의되지 않은 property 는 text 타입으로 입력될 수 있음

### sample data 추가

```
	curl -s -H 'Content-Type: application/json' -XPOST https://search-dnaoneteam-rfbr26ml4mip3bp3f3zeofkisu.ap-northeast-2.es.amazonaws.com/dna/_doc -d '
	{       
            "eventtime" : "2020-09-10 13:45:29",
            "country": "KR",
            "source_ip" : "222.105.146.133",
            "location": { 
                "lat": 37.2979833,
                "lon": 127.071765
            },
            "product": "2020 가을 신상"
      }'

``` 

### 지역기반 쿼리 

```
GET https://search-dnaoneteam-rfbr26ml4mip3bp3f3zeofkisu.ap-northeast-2.es.amazonaws.com/dna/_search
{
  "query": {
    "geo_bounding_box": { 
      "location": {
        "top_left": {
          "lat": 37.3,
          "lon": 127
        },
        "bottom_right": {
          "lat": 37.2,
          "lon": 127.1
        }
      }
    }
  }
}
```

### kibana dashboard map 확인
1. kibana dashboard
2. create new 
3. coordinate map 
4. index mapping 선택 
5. buckets 에서 'add'
6. geo coordicate 선택
7. geohash 선택
8. 위치정보를 가지고 있는 type property 선택(여기서는 location)
9. panel 저장 
10. dashboard 저장
11. 저장된 dashboard share 하여 embed link 획득

### 이슈
1. aws 에서 기본적으로 생성해주는 es 에서는 kibana zoom level 을 늘릴 수 없다. 
  - 기본 zoom level 은 8으로 (최대 15) 더 높은 레벨을 사용할 수 없다.

2. 별도의 kibana 연결을 시도하였으나 실패

  - 그리고 kibana.yml 파일을 통해서 kibana 구동 옵션을 조정해주어야 함
```yaml
map.tilemap.options.maxZoom: 15
map.tilemap.url: http://a.tile.openstreetmap.org/{z}/{x}/{y}.png
# https://tiles.elastic.co/v2/default/{z}/{x}/{y}.png?elastic_tile_service_tos=agree&my_app_name=kibana
```

3. aws 에서 제공해주는 kibana 에 별도의 wms 서버 연결을 위해서는 다음 설정을 추가
 - kibana advanced setting 에서 `visualization:tileMap:WMSdefaults` 을 수정해야함
```
{
  "enabled": true,
  "url": "<wms-map-server-url>",
  "options": {
    "format": "image/png",
    "transparent": true
  }
}
```


4. 보다 높은 zoom 레벨을 사용하려면 별도의 지도 서버 (WMS - Web Map Server) 를 연결해야함
  - custom kibana 설정이 필요함 => aws 기본은 사용 불가


### 참고 자료 


1. aws default elasticserach + kibana zoom level 관련 문의 사항 
 - https://discuss.opendistrocommunity.dev/search?q=zoom%20level
2. aws elasticsearch kibana wms manual
 - https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-kibana.html#es-kibana-map-server
3. date format 설정
 - https://www.elastic.co/guide/en/elasticsearch/reference/7.4/date.html#multiple-date-formats
4. kibana setting
 - https://www.elastic.co/guide/en/kibana/7.9/settings.html

