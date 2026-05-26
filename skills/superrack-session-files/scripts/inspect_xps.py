import argparse
import re
from pathlib import Path


def tokens(text):
    match = re.search(r'<Parameters Type="RealWorld">(.*?)</Parameters>', text, re.S)
    return match.group(1).split() if match else []


def tag(text, name):
    match = re.search(fr"<{name}>(.*?)</{name}>", text, re.S)
    return match.group(1).strip() if match else None


def attr_preset(text):
    match = re.search(r'<Preset Name="([^"]*)" GenericType="([^"]*)"', text)
    if not match:
        return None, None
    return match.group(1), match.group(2)


def inspect(path):
    data = Path(path).read_text(encoding="utf-8", errors="replace")
    preset_name, generic_type = attr_preset(data)
    print(f"file: {path}")
    print(f"top_preset: {preset_name!r} generic_type={generic_type!r}")
    print(f"top_plugin: {tag(data, 'PluginName')!r} subcomp={tag(data, 'PluginSubComp')!r}")

    for slot_match in re.finditer(r'<slot index="(\d+)">(.*?)</slot>', data, re.S):
        slot_index = int(slot_match.group(1))
        block = slot_match.group(2)
        preset_match = re.search(r'<plugin_preset Name="[^"]*"><!\[CDATA\[(.*?)\]\]></plugin_preset>', block, re.S)
        plugin_name = tag(block, "plugin_name")
        plugin_id = tag(block, "plugin_id")
        vendor = tag(block, "plugin_vendor")
        bypass = tag(block, "plugin_bypass")
        disabled = tag(block, "plugin_disabled")
        side_chain = tag(block, "plugin_side_chain")
        ignore_latency = tag(block, "plugin_ignore_latency")
        recall_safe = tag(block, "slot_recall_safe")

        if not preset_match and not plugin_name:
            continue

        print(
            f"slot {slot_index}: {plugin_name} {plugin_id} vendor={vendor} "
            f"bypass={bypass} disabled={disabled} side_chain={side_chain} "
            f"ignore_latency={ignore_latency} recall_safe={recall_safe}"
        )

        if preset_match:
            plugin_xml = preset_match.group(1)
            embedded_name, embedded_type = attr_preset(plugin_xml)
            realworld = tokens(plugin_xml)
            print(
                f"  embedded_preset={embedded_name!r} generic_type={embedded_type!r} "
                f"plugin={tag(plugin_xml, 'PluginName')!r} subcomp={tag(plugin_xml, 'PluginSubComp')!r} "
                f"tokens={len(realworld)}"
            )

            if plugin_id == "KPMM" and len(realworld) >= 435:
                print(
                    "  silk: "
                    f"out=({realworld[12]}, {realworld[30]}) "
                    f"low={realworld[371]} mid={realworld[372]} high={realworld[373]} "
                    f"gender={realworld[403]} extras=({realworld[405]}, {realworld[424]}, {realworld[434]})"
                )
            elif plugin_id == "QDZM" and len(realworld) >= 174:
                print(
                    "  f6: "
                    f"freqs={realworld[0:6]} q={realworld[8:14]} "
                    f"thresholds={realworld[56:62]} ranges={realworld[64:70]} "
                    f"enabled={realworld[168:174]}"
                )
            elif plugin_id == "DSAM":
                print(f"  deesser: tokens={realworld}")
            elif plugin_id == "MXVM":
                print(f"  rvox: tokens={realworld}")


def main():
    parser = argparse.ArgumentParser(description="Inspect a Waves SuperRack rack preset .xps export.")
    parser.add_argument("path")
    args = parser.parse_args()
    inspect(args.path)


if __name__ == "__main__":
    main()
