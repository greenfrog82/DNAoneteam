import React from 'react';
import Iframe from 'react-iframe'

function EsMap() {
    return (
        <Iframe url="https://search-dnaoneteam-rfbr26ml4mip3bp3f3zeofkisu.ap-northeast-2.es.amazonaws.com/_plugin/kibana/app/kibana#/visualize/edit/b557c110-f599-11ea-a7ff-6f0d64078204?embed=true&embed=true&_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))&_a=(filters:!(),linked:!f,query:(language:kuery,query:''),uiState:(mapCenter:!(37.19095471582608,127.27935791015626),mapZoom:10),vis:(aggs:!((enabled:!t,id:'1',params:(),schema:metric,type:count),(enabled:!t,id:'2',params:(autoPrecision:!t,field:location,isFilteredByCollar:!t,precision:2,useGeocentroid:!t),schema:segment,type:geohash_grid)),params:(addTooltip:!t,colorSchema:'Yellow%20to%20Red',heatClusterSize:1.5,isDesaturated:!t,legendPosition:bottomright,mapCenter:!(0,0),mapType:'Scaled%20Circle%20Markers',mapZoom:2,wms:(enabled:!f,options:(format:image%2Fpng,transparent:!t),selectedTmsLayer:(attribution:'%3Ca%20rel%3D%22noreferrer%20noopener%22%20href%3D%22https:%2F%2Fwww.openstreetmap.org%2Fcopyright%22%3EMap%20data%20%26%23169;%20OpenStreetMap%20contributors%3C%2Fa%3E',id:road_map,maxZoom:10,minZoom:0,origin:elastic_maps_service))),title:'default%20map',type:tile_map))"
            width="100%"
            height="100%"
            id="myId"
            display=""
            position="absolute" />
    )
}

export default EsMap;