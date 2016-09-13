import cairo
import pangocairo

import pango


class TextTRenderer():
    image = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720)

    def makeImage(self, listOfText, fontname, size, space_h=None):
        context = cairo.Context(self.image)
        pangocairo_context = pangocairo.CairoContext(context)
        pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        layout = pangocairo_context.create_layout()
        font = pango.FontDescription("{} {}".format(fontname, size))
        layout.set_font_description(font)
        size_x = 0
        size_y = 0
        for text in listOfText:
            layout.set_text(text)
            size = layout.get_size()
            size_x = max(size_x, size[0] / 1000.)
            dy = (size[1] / 1000.)
            size_y += (size[1] / 1000.)
        image = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(size_x), int(size_y))
        context = cairo.Context(image)
        pangocairo_context = pangocairo.CairoContext(context)
        pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        layout = pangocairo_context.create_layout()
        layout.set_font_description(font)
        yoffset = 0
        if space_h != None:
            dy = space_h
        for text in listOfText:
            # ((10, yoffset), text, font)
            layout.set_text(text)
            context.set_source_rgb(0, 0, 0)
            pangocairo_context.update_layout(layout)
            pangocairo_context.show_layout(layout)
            context.translate(0, dy)
        return image

    def makeImage_runnable(self, listOfText, fontname, size, space_h=None, color = (0,0,0)):
        context = cairo.Context(self.image)
        pangocairo_context = pangocairo.CairoContext(context)
        pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        layout = pangocairo_context.create_layout()
        font = pango.FontDescription("{} {}".format(fontname, size))
        layout.set_font_description(font)
        size_x = 0
        size_y = 0
        for text in listOfText:
            layout.set_text(text)
            size = layout.get_size()
            size_x = max(size_x, size[0] / 1000.)
            dy = (size[1] / 1000.)
            size_y += (size[1] / 1000.) if space_h is None else space_h
        if space_h != None:
            dy = space_h

        def getImage(idx):
            image = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(size_x), int(size_y))
            context = cairo.Context(image)
            pangocairo_context = pangocairo.CairoContext(context)
            pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
            layout = pangocairo_context.create_layout()
            layout.set_font_description(font)
            if space_h != None:
                dy = space_h
            offset = 0
            for text in listOfText:
                layout.set_text(text[0: max(idx - offset, 0)])
                context.set_source_rgb(color[0], color[1], color[2])
                pangocairo_context.update_layout(layout)
                pangocairo_context.show_layout(layout)
                context.translate(0, dy)
                offset += len(text)
            return image

        return getImage


    def makeImage_centered(self, listOfText, fontname, size, space_h=None, color = (0,0,0)):
        context = cairo.Context(self.image)
        pangocairo_context = pangocairo.CairoContext(context)
        pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        layout = pangocairo_context.create_layout()
        font = pango.FontDescription("{} {}".format(fontname, size))
        layout.set_font_description(font)
        size_x = 0
        size_y = 0
        for text in listOfText:
            layout.set_text(text)
            size = layout.get_size()
            size_x = max(size_x, size[0] / 1000.)
            dy = (size[1] / 1000.)
            size_y += (size[1] / 1000.)
        image = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(size_x), int(size_y))
        context = cairo.Context(image)
        pangocairo_context = pangocairo.CairoContext(context)
        pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        layout = pangocairo_context.create_layout()
        layout.set_font_description(font)
        context.save()
        yoffset = 0
        if space_h != None:
            dy = space_h
        for text in listOfText:
            # ((10, yoffset), text, font)
            layout.set_text(text)
            size = layout.get_size()
            context.set_source_rgb(color[0], color[1], color[2])
            context.translate((size_x - size[0]/1000.) / 2, yoffset)
            pangocairo_context.update_layout(layout)
            pangocairo_context.show_layout(layout)
            context.restore()
            context.save()
            yoffset += dy
        return image

    def makeImage_centered_runnable(self, listOfText, fontname, size, space_h=None, color=(0, 0, 0)):
        context = cairo.Context(self.image)
        pangocairo_context = pangocairo.CairoContext(context)
        pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        layout = pangocairo_context.create_layout()
        font = pango.FontDescription("{} {}".format(fontname, size))
        layout.set_font_description(font)
        size_x = 0
        size_y = 0
        sizes = []
        for text in listOfText:
            layout.set_text(text)
            size = layout.get_size()
            size_x = max(size_x, size[0] / 1000.)
            sizes.append(size[0] / 1000.)
            dy = (size[1] / 1000.)
            size_y += max(0 if space_h is None else space_h,size[1] / 1000.)

        def getImage(idx):
            image = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(size_x), int(size_y))
            context = cairo.Context(image)
            pangocairo_context = pangocairo.CairoContext(context)
            pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
            layout = pangocairo_context.create_layout()
            layout.set_font_description(font)
            context.save()
            yoffset = 0
            if space_h != None:
                dy = space_h
            offset = 0
            i = 0
            for text in listOfText:
            # ((10, yoffset), text, font)
                layout.set_text(text[0: max(idx - offset, 0)])
                size = sizes[i]
                context.set_source_rgb(color[0], color[1], color[2])
                context.translate((size_x - size) / 2, yoffset)
                pangocairo_context.update_layout(layout)
                pangocairo_context.show_layout(layout)
                context.restore()
                context.save()
                offset += len(text)
                yoffset += dy
                i+=1
            return image

        return getImage
