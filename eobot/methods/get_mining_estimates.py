from ..lib.eobot_config import EobotConfig, get_config
from ..lib.eobot_errors import NoUserIdError
from ..lib.eobot_request import EobotRequest
from .get_user_id import perform_request as get_user_id


def perform_request(config=None, request=None):
    """
    Retrieves the current estimated mining profits for the current user, in US Dollar per month

    :param config : (Optional) Configuration to use, will default to the global config if not provided
    :type config : EobotConfig|str|None

    :param request : (Optional) Request object to use, will default to a new one if not provided
    :type request : EobotRequest|None

    :rtype : dict
    """
    if request is None:
        request = EobotRequest()
    elif not isinstance(request, EobotRequest):
        raise ValueError("Invalid request, must be a EobotRequet")

    if config is None or isinstance(config, str):
        config = get_config(config)
    elif not isinstance(config, EobotConfig):
        raise ValueError("Invalid config, must be a EobotConfig")

    try:
        auth = config.get_authentication(True)
    except NoUserIdError:
        config.set_user_id(get_user_id(config=config, request=request.clone()))
        auth = config.get_authentication(True)

    request.set_parameter("idestimates", auth.user_id)

    result = request.perform_request()

    for miner in result.keys():
        result[miner] = float(result[miner])

    return result
