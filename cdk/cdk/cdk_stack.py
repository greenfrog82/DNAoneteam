from aws_cdk import (
    core, 
    aws_s3 as s3, 
    aws_cloudfront as cfn, 
    aws_cloudfront_origins as origins, 
)


class CdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        bucket = s3.Bucket(self, 'dna-front', versioned=True,)
        cfn.Distribution(self, 'dna-front-deploy',
            default_behavior=cfn.BehaviorOptions(origin=origins.S3Origin(bucket))
        )
