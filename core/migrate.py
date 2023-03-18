import os
from asyncio import sleep
from typing import List
from .logger import logger
from .settings import settings
from tortoise import fields, models
from tortoise.transactions import in_transaction


class Migrate(models.Model):
    id = fields.BigIntField(pk=True)
    file = fields.CharField(max_length=1024)


async def migrate():
    await sleep(3)
    # Инициализация таблицы регистрирующей миграции
    async with in_transaction("default") as conn:
        await conn.execute_script(
            "create table if not exists \"migrate\"(\"id\" serial primary key, \"file\" varchar(1024));"
        )

    script_files: List[str] = os.listdir(settings.DB_MIGRATE_PATH)
    script_db: Migrate = await Migrate.filter().order_by("-id").first()
    if script_db is None:
        unregister_script_files = script_files
    else:
        unregister_script_files = script_files[(script_files.index(script_db.file) + 1):]

    logger.info(f"Найдено {len(unregister_script_files)} изменений ({unregister_script_files})")
    for script_file in sorted(unregister_script_files):
        sql_script = open(file=f"{settings.DB_MIGRATE_PATH}{os.sep}{script_file}", mode="r").read()
        async with in_transaction("default") as t_conn:
            await t_conn.execute_script(sql_script)
            await Migrate.create(file=script_file)

