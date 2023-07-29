# This Bucket is not the same as the state bucket
# It will be created by terraform after apply
resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.bucket_name
  acl    = "private"
  force_destroy = true
}

output "name" {
  value = aws_s3_bucket.s3_bucket.bucket
}