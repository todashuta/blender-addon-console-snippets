bl_info = {
    "name": "Console Snippets",
    "author": "todashuta",
    "version": (0, 0, 2),
    "blender": (3, 6, 0),
    "location": "Console Context Menu",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Console"
}


import bpy


TEXT_NAME = "snippets.txt"


class ConsoleSnippetsAddExample(bpy.types.Operator):
    bl_idname = "console.console_snippets_add_example"
    bl_label = "Console Snippets Add Example Text"

    @classmethod
    def poll(cls, context):
        return bpy.data.texts.get(TEXT_NAME) is None

    def execute(self, context):
        text = bpy.data.texts.new(TEXT_NAME)
        text.write('''\
# #で始まる行、空行、空白だけの行は無視されます

image size list | for i in D.images: i.size[:],i.name
for active objects | for ob in C.selected_objects: C.view_layer.objects.active = ob; print(C.active_object)
clear custom split normals|for ob in C.selected_objects: C.view_layer.objects.active = ob; bpy.ops.mesh.customdata_custom_splitnormals_clear(),ob.name
''')
        return {"FINISHED"}


class ConsoleSnippetsInsertText(bpy.types.Operator):
    bl_idname = "console.console_snippets_insert_text"
    bl_label = "Console Snippets Insert Text"

    text: bpy.props.StringProperty(name="Text", default="")

    @classmethod
    def description(cls, context, properties):
        return f"code: `{properties.text}`"

    @classmethod
    def poll(cls, context):
        return bpy.ops.console.insert.poll()

    def execute(self, context):
        bpy.ops.console.clear_line()
        return bpy.ops.console.insert(text=self.text)


def draw_func(self, context):
    layout = self.layout
    layout.separator()
    if (snippets := bpy.data.texts.get(TEXT_NAME)) is None:
        layout.operator(ConsoleSnippetsAddExample.bl_idname)
        return

    for l in snippets.lines:
        s = l.body.strip()
        if s == '':
            continue
        if s.startswith('#'):
            continue
        items = [i.strip() for i in s.split('|', 1)]
        if len(items) != 2:
            continue
        op = layout.operator(ConsoleSnippetsInsertText.bl_idname, text=items[0])
        op.text = items[1]


classes = (
        ConsoleSnippetsInsertText,
        ConsoleSnippetsAddExample,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.CONSOLE_MT_context_menu.append(draw_func)


def unregister():
    bpy.types.CONSOLE_MT_context_menu.remove(draw_func)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
