# 导入随机模块
import random
# 导入 playwright 模块，用于自动化浏览器操作
from playwright.sync_api import sync_playwright

# 定义一个函数，用于在文本前面添加一个随机的短语
def add_random_content(text):
    # 随机选择 “我觉得”、“我认为”、“其实”、“实际上” 中的一个短语
    phrases = ["我觉得是", "我认为是", "我认为要","我觉得要"]
    random_phrase = random.choice(phrases)
    # 在文本前面添加短语，并在后面添加一个随机的标点符号
    result = random_phrase + text +random.choice(["。"," ","..","~"])
    # 返回结果
    return result

# 定义一个函数，用于自动回答问题，接受账号和密码作为参数
def answer(account, password):
    # 使用 playwright 模块创建一个浏览器对象
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        # 创建一个浏览器上下文对象
        context = browser.new_context()
        # 创建一个网页对象
        page = context.new_page()
        # 打开指定的网址
        page.goto(
            "https://qah5.zhihuishu.com/qa.html#/web/home/1000009213?role=2&recruitId=164977&fromUrl=2&VNK=bcf76f0d")
        # 点击输入手机号的框，并输入账号
        page.get_by_placeholder("请输入手机号").click()
        page.get_by_placeholder("请输入手机号").fill(f"{account}")
        # 点击输入密码的框，并输入密码
        page.get_by_role("textbox", name="请输入密码").click()
        page.get_by_role("textbox", name="请输入密码").fill(f"{password}")
        # 点击登录按钮
        page.get_by_text("登 录").click()

        # 点击话题讨论按钮
        page.get_by_text("话题讨论").click()

        # 等待问题列表出现
        page.wait_for_selector(".question-content.ZHIHUISHU_QZMD")
        # 获取所有问题元素的列表
        elements = page.query_selector_all('.question-content.ZHIHUISHU_QZMD')
        # 打印问题的数量
        print(f"共{len(elements)}个回答")
        # 初始化计数器，用于记录回答的序号
        count = 0

        # 遍历每个问题元素
        for element in elements:
            # 点击问题元素，打开一个新的网页对象
            with page.expect_popup() as page1_info:
                element.click()
            page1 = page1_info.value
            # 定义一个选择器，用于定位问题内容的元素
            selector = "li:nth-child(1) div:nth-child(3) p:nth-child(1) span:nth-child(1)"
            # 等待该元素出现
            page1.wait_for_selector(selector)
            # 获取该元素的句柄对象
            element_handle = page1.locator(selector)
            # 如果该元素存在，说明问题有内容，否则跳过该问题
            if element_handle is not None:
                # 获取该元素的文本内容，即问题内容
                span_content = element_handle.text_content()
                # 如果网页中有“我来回答”的按钮，说明该问题未回答，否则跳过该问题
                if page1.locator("//span[contains(text(),'我来回答')]").count() == 1:
                    # 打印当前未回答的问题序号，并点击“我来回答”按钮
                    print(f"{count}号未回答，开始回答问题")
                    page1.get_by_text("我来回答").click()
                    # 点击输入回答的框，并等待一段随机的时间
                    page1.get_by_placeholder("请输入您的回答").click()
                    page1.wait_for_timeout(2500 + random.randint(0, 1000))
                    # 在输入框中填入随机生成的回答内容，并等待一段随机的时间
                    page1.get_by_placeholder("请输入您的回答").fill(f"{add_random_content(span_content)}")
                    page1.wait_for_timeout(2500 + random.randint(0, 1000))
                    # 点击“立即发布”按钮，并等待一段随机的时间
                    page1.get_by_text("立即发布").click()
                    page1.wait_for_timeout(2500 + random.randint(0, 1000))
                    # 关闭当前网页对象
                    page1.close()
                    # 计数器加一
                    count = count + 1
                else:
                    # 打印当前已回答的问题序号，并关闭当前网页对象
                    count = count + 1
                    print(f"{count}号问题已回答")
                    page1.close()
            else:
                # 打印未找到指定元素的信息，并关闭当前网页对象
                print("未找到指定元素")
                page1.close()

        # 关闭浏览器对象
        browser.close()

# 如果是主程序，执行以下代码
if __name__ == '__main__':
    # 输入账号和密码
    account = input("请输入账号：")
    password = input("请输入密码：")
    # 调用 answer 函数，传入账号和密码
    answer(account,password)
