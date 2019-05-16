import random,os
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont,ImageFilter

class CreateCode:
    def __init__(self,size=(120,30),img_type="GIF",mode="RGB",bg_color=(255,255,255),
                 fg_color=(0,0,255),font_size=18,font_type="calibri.ttf",length=4,
                 draw_lines=True,n_line = (1,2),draw_points=True,point_chance=2):
        '''
            @todo: 生成验证码图片
            @param size: 图片的大小，格式（宽，高），默认为(120, 30)
            @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
            @param mode: 图片模式，默认为RGB
            @param bg_color: 背景颜色，默认为白色
            @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
            @param font_size: 验证码字体大小
            @param font_type: 验证码字体，默认为 calibri.ttf
            @param length: 验证码字符个数
            @param draw_lines: 是否划干扰线
            @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
            @param draw_points: 是否画干扰点
            @param point_chance: 干扰点出现的概率，大小范围[0, 100]
            @return: [0]: PIL Image实例
            @return: [1]: 验证码图片中的字符串
            '''
        self.size=size
        self.img_type=img_type
        self.mode=mode
        self.bg_color=bg_color
        self.fg_color=fg_color
        self.font_size = font_size
        self.font_type =font_type
        self.length = length
        self.draw_lines =draw_lines
        self.point_chance = point_chance
        self.n_line=n_line
        self.draw_points=draw_points
        #执行初始化函数
        self.getAllChar()
        self.initPaint()
        self.get_chars()

    def initPaint(self):
        '''
        初始画布
        :return:
        '''
        self.width,self.height=self.size
        self.img = Image.new(self.mode,self.size,self.bg_color)
        self.draw = ImageDraw.Draw(self.img)#创建画笔

    def getAllChar(self):
        '''
        获取所有字符串
        :return:
        '''
        _letter_cases = "zxcvbnmasdfghjklqwertyuiop"
        _upper_cases = _letter_cases.upper()
        _numbers = ''.join(map(str, range(0, 9)))
        _chinese=self.GBK2312()
        # 获取所有的字符
        self.init_chars = ''.join((_letter_cases, _upper_cases, _numbers,_chinese))

    def GBK2312(self):
        """
        生成随机中文字符
        :return: 返回10个随机中文字符集
        """
        all_str=[]
        for i in range(10):
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xfe)
            val = f'{head:x}{body:x}'
            one_str = bytes.fromhex(val).decode('gb18030')
            all_str.append(one_str)
        return ''.join(all_str)

    def get_chars(self):
        '''生成给定长度的字符串，返回裂变格式'''
        return random.sample(self.init_chars,self.length)#从给定字符串中获取出随机字符

    def create_lines(self):
        '''绘制干扰线'''
        line_num = random.randint(*self.n_line)#从元组中获取线条数目
        for i in range(line_num):
            #起始点
            begin = (random.randint(0,self.size[0]),random.randint(0,self.size[1]))#在图片中随机位置
            end = (random.randint(0,self.size[0]),random.randint(0,self.size[1]))#在图片中随机位置
            self.draw.line([begin,end],fill=(0,0,0))

    def create_point(self):
        '''绘制干扰点'''
        chance = min(100,max(0,int(self.point_chance)))#大小限制在point_chance到100
        for w in range(self.width):
            for h in range(self.height):
                tmp = random.randint(0,100)
                if tmp > 100-chance:
                    self.draw.point((w,h),fill=(0,0,0))

    def create_strs(self):
        '''绘制验证码'''
        c_chars = self.get_chars()
        strs = ' %s '%' '.join(c_chars)

        font = ImageFont.truetype(self.font_type,self.font_size)
        font_width,font_height = font.getsize(strs)

        self.draw.text(((self.width-font_width)/3,(self.height-font_height)/3),strs,font=font,fill=self.fg_color)

        return ''.join(c_chars)

    def get_img(self,use_bytes_io=True):
        if self.draw_lines:
            self.create_lines()
        if self.draw_points:
            self.create_point()
        strs = self.create_strs()
        #图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = self.img.transform(self.size, Image.PERSPECTIVE, params)  # 创建扭曲

        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

        if use_bytes_io:
            out=BytesIO()
            img.save(out,format=self.img_type)
            return strs,out

        return strs,img

if __name__=="__main__":
    verify_image = CreateCode(font_type='msyh.ttc', img_type='PNG')
    code,image=verify_image.get_img()

    #print(image.getvalue())

    #print(image.show())
    print(code)



