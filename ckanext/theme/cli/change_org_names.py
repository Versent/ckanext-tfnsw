from collections import OrderedDict
import os
import pathlib
import pkg_resources
import shutil
import subprocess
import time

import babel.messages.pofile
import ckan
import click


branding = OrderedDict()
branding["group"] = "topic"
branding["Group"] = "Topic"
branding["an organization"] = "content"
branding["an Organization"] = "Content"
branding["An organization"] = "Content"
branding["An Organization"] = "Content"
branding["organization"] = "content"
branding["Organization"] = "Content"


preserve = [
    "{organization}",
    "organization_name",
    "group_name",
    "{group}",
]


def replace_branding(msgid):
    if isinstance(msgid, tuple):
        return tuple([replace_branding(m) for m in list(msgid)])
    else:
        for pp in preserve:
            msgid = msgid.replace(pp, pp.upper())
        for bb in branding:
            msgid = msgid.replace(bb, branding[bb])
        for pp in preserve:
            msgid = msgid.replace(pp.upper(), pp)
        return msgid


@click.command()
def tfnsw_change_org_names():
    src = pathlib.Path(pkg_resources.resource_filename("ckan.i18n",
                                                       "ckan.pot"))
    with src.open("r", encoding="utf-8") as fd:
        poin = babel.messages.pofile.read_po(fd)

    for msg in poin:
        msg.string = replace_branding(msg.id)

    sjs = pathlib.Path(
        pkg_resources.resource_filename("ckan", "public/base/i18n/en_GB.js"))
    shutil.copy(str(sjs), str("/tmp/en_GB.js"))
    for lang in ["en_US", "en_GB", "en_AU"]:

        dest = src.parent / lang / "LC_MESSAGES" / "ckan.po"
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as fd:
            babel.messages.pofile.write_po(fd, poin)
        with dest.open("rb") as fd:
            data = fd.readlines()
        data.insert(10, b'"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n')
        with dest.open("wb") as fd:
            data = fd.writelines(data)

        cpath = pathlib.Path(ckan.__file__).parent.parent
        os.chdir(str(cpath))
        subprocess.check_output(
            "python setup.py compile_catalog --locale {} --use-fuzzy".format(lang),
            shell=True)

        time.sleep(1)
        shutil.copy("/tmp/en_GB.js", str(sjs.with_name("{}.js".format(lang))))
