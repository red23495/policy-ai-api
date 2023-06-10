import requests
from IPython import display
import json
from io import StringIO


class PolicyAI:

    def __init__(self, *, url: str):
        self.url = url.strip().strip('/')

    def _display_response(self, response):
        try:
            display.display(display.HTML(
                f'<pre>{json.dumps(response.json(), indent=2)}</pre>'
            ))
        except:
            display.display(display.HTML(response.content.decode('utf-8')))

    def _upload_chart(self, *, path: str, name: str, version: str, chart: str):
        response = requests.post(
            f'{self.url}/chart/upload/',
            data={
                'chart.path': path,
                'chart.name': name,
                'version': version,
            },
            files={
                'file': ('chart', chart)
            }
        )
        return response

    def upload_chart(self, *, path: str, name: str, version: str, chart: str):
        response = self._upload_chart(
            path=path, name=name, version=version, chart=chart
        )
        self._display_response(response)
        return response
    
    def upload_plotly(self, figure, *, name: str, path: str, version: str):
        buffer = StringIO()
        figure.write_html(buffer, include_plotlyjs=False, full_html=False)
        chart = buffer.getvalue()
        return self.upload_chart(
            path=path, name=name, version=version, chart=chart
        )
