from Bot.Bot import AutoBot
import time
import Bot.constants as const


def run(search):
    with AutoBot() as test:
        test.open_url(const.base_url)
        test.select_state(const.state)
        test.select_county(const.county)
        time.sleep(5)
        test.search_bar(search)
        test.search_per_page(const.posts)
        test.all_headings(const.print_data)
        test.download_pdf()


run("Minimum trees per lot")
#run("vegetation")
#run("trees allowed on lot")
#run("tree types")
#run("native")
#run("tree height")

time.sleep(5)
