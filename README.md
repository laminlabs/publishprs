# publishprs: Publish pull requests in a private repo to a public repo

Install:

```bash
pip install publishprs
```

Publish a PR:

```python
from publishprs import Publisher
publisher = Publisher(
    source_repo="https://github.com/laminlabs/laminhub",
    target_repo="https://github.com/laminlabs/laminhub-public",
    db="laminlabs/lamin-site-assets"
)
url = publisher.publish(pull_id=3820)
print(f"Published to: {url}")
```
