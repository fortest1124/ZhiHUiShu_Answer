import random
from playwright.sync_api import sync_playwright
def add_random_content(text):
    # 随机选择 “我觉得”、“我认为”、“其实”、“实际上” 中的一个短语
    phrases = ["我觉得是", "我认为是", "我认为要","我觉得要"]
    random_phrase = random.choice(phrases)
    result = random_phrase + text +random.choice(["。"," ","..","~"])
    return result

def answer(account, password):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(
            "https://qah5.zhihuishu.com/qa.html#/web/home/1000009213?role=2&recruitId=164977&fromUrl=2&VNK=bcf76f0d")
        # cookies = context.cookies()
        # Path("cookies.json").write_text(json.dumps(cookies))
        page.get_by_placeholder("请输入手机号").click()
        page.get_by_placeholder("请输入手机号").fill(f"{account}")
        page.get_by_role("textbox", name="请输入密码").click()
        page.get_by_role("textbox", name="请输入密码").fill(f"{password}")
        page.get_by_text("登 录").click()

        page.get_by_text("话题讨论").click()

        # 获取问题列表
        page.wait_for_selector(".question-content.ZHIHUISHU_QZMD")
        elements = page.query_selector_all('.question-content.ZHIHUISHU_QZMD')
        print(f"共{len(elements)}个回答")
        count = 0

        for element in elements:
            with page.expect_popup() as page1_info:
                element.click()
            page1 = page1_info.value
            selector = "li:nth-child(1) div:nth-child(3) p:nth-child(1) span:nth-child(1)"
            page1.wait_for_selector(selector)
            element_handle = page1.locator(selector)
            if element_handle is not None:
                span_content = element_handle.text_content()
                if page1.locator("//span[contains(text(),'我来回答')]").count() == 1:
                    print(f"{count}号未回答，开始回答问题")
                    page1.get_by_text("我来回答").click()
                    page1.get_by_placeholder("请输入您的回答").click()
                    page1.wait_for_timeout(2500 + random.randint(0, 1000))
                    page1.get_by_placeholder("请输入您的回答").fill(f"{add_random_content(span_content)}")
                    page1.wait_for_timeout(2500 + random.randint(0, 1000))
                    page1.get_by_text("立即发布").click()
                    page1.wait_for_timeout(2500 + random.randint(0, 1000))
                    page1.close()
                    count = count + 1
                else:
                    count = count + 1
                    print(f"{count}号问题已回答")
                    page1.close()
            else:
                print("未找到指定元素")
                page1.close()

        browser.close()
if __name__ == '__main__':
    account = input("请输入账号：")
    password = input("请输入密码：")
    answer(account,password)

