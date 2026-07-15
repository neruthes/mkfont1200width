# mkfont1200width

与其寻找一个 1200 宽度字体，不如创造一个 1200 宽度字体。

Small Python script to modify a font.
Any 1000-width glyph will become 1200-width.


## Dependencies

See below and use pip or other package manager to install.

```
$ tree _venv/lib -L3
_venv/lib
└── python3.13
    └── site-packages
        ├── fontTools
        ├── fonttools-4.61.1.dist-info
        ├── pip
        └── pip-26.0.1.dist-info
```


## Usage

- Set up venv (optional)
- `mkdir -p build`
- `python3 src/convert.py path/to/input/font.ttc build/Wide1200-font.ttc`


## Usage Example

```sh
mkdir -p build
fc-list | grep NotoSerifCJK | cut -d: -f1 | sort -u | while read -r fn; do
    python3 src/convert.py "$fn" build/Wide1200-"$(basename "$fn")"
done
wait
```


## Notes

- Now only TTC. Maybe OTF/TTF in future? Noto CJK has only TTC so I did not care other formats.


## Copyright

Copyright (c) 2026 Nerthes. Released with the MIT license (https://mit-license.org/).
