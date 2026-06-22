SECRET = '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'
ANOTHER_SECRET = 'glpat-mZj8TyXrdLnzuXqQ4ZqX'

def secret_hider(s):
    return "*"*len(s)

print("Very secure!")
print(f"SECRET = {secret_hider(SECRET)}")
print(f"ANOTHER_SECRET = {secret_hider(ANOTHER_SECRET)}")
