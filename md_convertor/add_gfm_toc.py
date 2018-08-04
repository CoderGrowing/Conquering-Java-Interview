import os
import re

from .add_space import get_md_files_list


TOC_SUFFIX = "<!-- GFM-TOC -->\n"
TOC_POSTFIX = TOC_SUFFIX + "\n\n"


def get_original_lines_without_toc(filename):
    """
    获取指定文件名中的内容，并去除文件中原本可能存在的 GFM-TOC
    """
    with open(filename, "r", encoding="UTF-8") as f:
        lines = f.readlines()

        lines_without_toc = list()
        toc_flag = 0            # TOC_SUFFIX 和 TOC_POSTFIX 记为 TOC_FLAG
        for line in lines:
            if line == TOC_SUFFIX:
                global TOC_POSTFIX
                TOC_POSTFIX = TOC_SUFFIX    # 如果原本已有TOC，就不多加两行空行了
                toc_flag += 1
                continue

            if toc_flag == 2:
                lines_without_toc.append(line)

    return lines_without_toc


def get_subtitles(lines):
    subtitles = list()

    for line in lines:
        if line.startswith("#"):
            subtitles.append(line.strip())

    return subtitles


def convert_to_gfm_spec(lines):
    """
    将输入进来的每一行标题形式转化为 GFM-TOC 的标准，具体为：
        特殊符号去掉
        空格转化为连字符 -
        字幕转化为小写
    转换后的形式如：  * [一、Java 基础](#一java-基础)
    :param lines: 可迭代类型，其中每一个元素都是一行标题
    :return: 转换后的 GFM-TOC 格式
    """
    special_char = re.compile("[.?!,，。？！=、]")
    blank = re.compile(" ")
    gfm_subtitles = list()
    indent = 4

    for line in lines:
        line_without_pound = line.replace("#", "").strip()         # 进去掉#符号的标题用于目录文字的展示
        indent_level = indent * (line.count("#") - 1)              # 不同级别的标题有不同的缩进

        line = line.replace("#", "").strip()
        line = re.sub(special_char, "", line)
        line = re.sub(blank, "-", line)
        line = line.lower()

        gfm_subtitles.append(
            indent_level * " " +
            "* [{}]({})\n".format(line_without_pound, "#" + line)
        )

    return gfm_subtitles


def write_toc_to_file(filename, original_lines, toc):
    with open(filename, "w", encoding="UTF-8") as f:
        f.write(TOC_SUFFIX)
        for toc_line in toc:
            f.write(toc_line)
        f.write(TOC_POSTFIX)

        for original_line in original_lines:
            f.write(original_line)


def main():
    md_files = get_md_files_list()

    for md_file in md_files:
        original_lines = get_original_lines_without_toc(md_file)
        subtitles = get_subtitles(original_lines)
        gfm_toc = convert_to_gfm_spec(subtitles)
        write_toc_to_file(md_file, original_lines, gfm_toc)
        print("Add GFM-TOC for: {}".format(os.path.basename(md_file)))

    print("Add GFM-TOC done!\n")


if __name__ == '__main__':
    main()
