from lxml import etree, objectify

E = objectify.ElementMaker(annotate=False)
anno_tree = E.annotation(
    E.folder('VOC2007'),
    E.filename('hi'),
    E.size(
        E.width(str(100)),
        E.height(str(100)),
        E.depth(str(3))
    ),
    E.segmented('0'),
    E.object(
        E.name('1'),
        E.pose('Unspecified'),
        E.truncated('0'),
        E.difficult('0'),
        E.bndbox(
            E.xmin(1),
            E.ymin(2),
            E.xmax(3),
            E.ymax(4)
        )
    )
)

print type(anno_tree)

etree.ElementTree(anno_tree).write("test.xml", pretty_print=True)

anno_tree2 = objectify.parse("test.xml").getroot()
print type(anno_tree2.getchildren()[2])
print type(anno_tree2)
anno_tree_son = E.object(
    E.name('2'),
    E.pose('Unspecified'),
    E.truncated('0'),
    E.difficult('0'),
    E.bndbox(
        E.xmin(2),
        E.ymin(3),
        E.xmax(4),
        E.ymax(5)
    )
)
anno_tree2.append(anno_tree_son)
etree.ElementTree(anno_tree2).write("test2.xml", pretty_print=True)