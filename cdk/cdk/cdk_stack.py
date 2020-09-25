from aws_cdk import (
    core, 
    aws_s3 as s3, 
    aws_cloudfront as cfn,
    aws_iam as iam,
    # aws_cloudfront_origins as origins, 
)


class CdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        source_bucket = s3.Bucket(self, 'DnaFront', versioned=True,)
        source_bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[source_bucket.arn_for_objects("*")],
            principals=[iam.AnyPrincipal()],
        ))

        distribution = cfn.CloudFrontWebDistribution(self, "DnaFrontEndDistributor",
            origin_configs=[
                cfn.SourceConfiguration(
                    s3_origin_source=cfn.S3OriginConfig(
                        s3_bucket_source=source_bucket
                    ),
                    behaviors=[cfn.Behavior(is_default_behavior=True)]
                )
            ],
            default_root_object='index.html',
            viewer_protocol_policy=cfn.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            error_configurations=[
                cfn.CfnDistribution.CustomErrorResponseProperty(error_code=403, response_code=200, error_caching_min_ttl=5, response_page_path='/index.html'),
                cfn.CfnDistribution.CustomErrorResponseProperty(error_code=404, response_code=200, error_caching_min_ttl=5, response_page_path='/index.html'),
            ],
        )
