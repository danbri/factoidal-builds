#!/usr/bin/env python3
"""Does a published @factoidal/core version name this web release?

Usage: npm-names-release.py TAG SHA
  TAG  the web release tag, build-<12 hex>-web
  SHA  its 40-hex core commit

Reads every version of the package on registry.npmjs.org and the
`package/l4-assets/version.json` inside its tarball. A version names the
release when that file's `release` ends with TAG or its `gitSha` is SHA.

Exit 0: at least one version names it (the versions are printed).
Exit 1: no version names it.
Exit 2: the registry or a tarball could not be read (the caller must
        treat this as "named": fail closed).

danbri/factoidal issue 1038, P7: a forced rebuild must never replace a
web release that a published version.json names.
"""
import io, json, os, sys, tarfile, urllib.request

PKG = os.environ.get('NPM_PKG', '@factoidal/core')
REGISTRY = os.environ.get('NPM_REGISTRY', 'https://registry.npmjs.org')


def get(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def main():
    tag, sha = sys.argv[1], sys.argv[2]
    try:
        doc = json.loads(get(f"{REGISTRY}/{PKG.replace('/', '%2F')}"))
    except Exception as e:  # noqa: BLE001
        print(f'cannot read {PKG} from {REGISTRY}: {e}', file=sys.stderr)
        return 2
    named = []
    for ver, meta in sorted(doc.get('versions', {}).items()):
        url = meta.get('dist', {}).get('tarball')
        if not url:
            print(f'{PKG}@{ver}: no dist.tarball', file=sys.stderr)
            return 2
        try:
            tf = tarfile.open(fileobj=io.BytesIO(get(url)), mode='r:gz')
            try:
                member = tf.extractfile('package/l4-assets/version.json')
            except KeyError:
                continue  # 0.8.x and older: no l4-assets/version.json
            v = json.load(member)
        except Exception as e:  # noqa: BLE001
            print(f'{PKG}@{ver}: cannot read l4-assets/version.json: {e}', file=sys.stderr)
            return 2
        if str(v.get('release', '')).endswith(tag) or v.get('gitSha') == sha:
            named.append(ver)
    if named:
        print(f'{tag} is named by {PKG} ' + ', '.join(named))
        return 0
    print(f'{tag} is named by no version of {PKG}')
    return 1


if __name__ == '__main__':
    sys.exit(main())
