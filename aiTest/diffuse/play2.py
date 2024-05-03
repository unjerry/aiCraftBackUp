from huggingface_hub import cached_assets_path

assets_path = cached_assets_path(
    library_name="datasets", namespace="SQuAD", subfolder="download"
)
something_path = (
    assets_path / "something.json"
)  # Do anything you like in your assets folder !

print(assets_path)
print(something_path)
