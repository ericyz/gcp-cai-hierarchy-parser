# Usage
```
ORG_ID=<your-org-id>
GCS_BUCKET=<bucketname>

gcloud asset export --output-path=gs://${GCS_BUCKET}/resource_inventory.json --content-type=resource --organization=${ORG_ID} 

gsutil cp gs://${GCS_BUCKET}/resource_inventory.json resource_inventory.json
pip3 install -r requirements.txt

python3 main.py --cai-resource-file-path=$(pwd)/resource_inventory.json
```