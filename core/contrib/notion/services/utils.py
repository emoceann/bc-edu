from typing import TypeVar

from core.contrib.notion.services.settings import settings
from .notion import NotionComment, Notion, logger
from core.contrib.notion.dao import CommentsNotion
from app.account import services as account_services
from app.telegram import deps as tg_deps


TitleList = TypeVar('TitleList', bound=list[str])
ResultData = TypeVar('ResultData', bound=list)


def format_notion_comments_to_csv(comments: list[NotionComment]) -> tuple[TitleList, ResultData]:
    title_list = ['Статья', 'Автор', 'Комментарий', 'Дата']
    result = []

    for notion_comment in comments:
        comment = notion_comment.comment
        user = notion_comment.user

        comment_text = ''

        for elem in notion_comment.comment.rich_text:
            comment_text = elem.plain_text

        row = [comment.parent.block_id, f'{user.name} {user.person.email}', comment_text, comment.created_time]
        result.append(row)

    return title_list, result


async def get_user_comments():
    page_ids = settings.NOTION_PAGE_IDS.split(',')
    notion_parse = Notion()
    comments = await notion_parse.get_comments_from_page(page_ids)
    if not comments:
        logger.info('Нет комментов')
        return

    for i in comments:
        if not await check_page_exists_by_id_user_email(i.comment.parent.block_id, i.user.person.email):
            notion_comment = await create_notion_comment(
                page_id=i.comment.parent.block_id, comment_id=i.comment.id, email=i.user.person.email, message=i.comment.rich_text
            )
            user = await notion_comment.user_email.get()
            await tg_deps.bot.send_message(user.id, 'Криптан💪! На твой счет начислено 100 Banana-Coins🟡 за коммент под статьей!')
            await account_services.update_user_fields(user.id, {'coins': 100})






async def check_page_exists_by_id_user_email(page_id: str, email: str):
    return await CommentsNotion.exists(page_id=page_id, user_email_id=email)

async def create_notion_comment(page_id: str, comment_id: str, email: str, message: str):
    return await CommentsNotion.create(page_id=page_id, comment_id=comment_id, user_email_id=email, message=message)