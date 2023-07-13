import pathlib
import requests
import json
import re

root = pathlib.Path(__file__).parent.resolve()


def replace(content, section, chunk, inline=False):
    chunk = '<!--START_SECTION:{}-->{}<!--END_SECTION:{}-->'.format(section, "\n{}\n".format(chunk), section)
    return re.sub(r'<!\-\-START_SECTION:{}\-\->((.|\n)*)<!\-\-END_SECTION:{}\-\->'.format(section, section), chunk, content)


def fetch(section):
    filtered = []
    res = requests.get("https://pub-8a6db429542c44318cca163b0371a391.r2.dev/portfolio-assets/tarun-pull-requests.json")
    response = json.loads(res.text)
    for key in response.keys():
        # only append if key doesn't start with 'tarun7singh'
        if not key.startswith('tarun7singh'):
            filtered.append(response[key])
    return filtered


if __name__ == '__main__':
    readme_path = root / 'README.md'
    readme = readme_path.open().read()
    repositories = fetch("open-source")
    entries_md = ""
    for i in range(len(repositories)):
        entries_md += f'* [{repositories[i][0]["repository_name"]}]({repositories[i][0]["repository_url"]})\n'
        entries_md += ''.join(
            ['  * [{title}]({url}) \n'.format(**repository) for repository in repositories[i]]
        )

    # Update entries
    rewritten_entries = replace(readme, 'open-source', entries_md)
    readme_path.open('w').write(rewritten_entries)
