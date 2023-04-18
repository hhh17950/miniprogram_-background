from dependencies import get_cache_collect


async def get_many_cache(mongodb_manager, name):
    cache_collect = get_cache_collect(mongodb_manager)
    result = cache_collect.find({"name": name})
    data = await result.to_list(length=None)
    return data


async def get_cache(mongodb_manager, name):
    cache_collect = get_cache_collect(mongodb_manager)
    result = await cache_collect.find_one({"name": name})
    return result


async def update_cache(mongodb_manager, name, data, upsert=True):
    cache_collect = get_cache_collect(mongodb_manager)
    await cache_collect.update_one(
        {"name": name},
        {'$set': data},
        upsert=upsert
    )


async def save_cache(mongodb_manager, datas: list):
    cache_collect = get_cache_collect(mongodb_manager)
    await cache_collect.insert_many(datas)


async def delete_cache(mongodb_manager, name):
    cache_collect = get_cache_collect(mongodb_manager)
    await cache_collect.delete_one(
        {"name": name},
    )
