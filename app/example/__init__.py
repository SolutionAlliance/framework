from app.example.views.export_view import ExampleView


def example_url_pattern(api,app):
    """
    mes_url_pattern
    @param api:
    @param app:
    @return:
    """
    '''--------------------------- 示例计划 -----------------------'''
    # 示例视图路由注册
    api.add_resource(ExampleView, '/example/<username>')