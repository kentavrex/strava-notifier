import logging
import requests
from pydantic import BaseModel


class CourseInfo(BaseModel):
    name: str
    limit: int
    available: int


class MyITMOService:
    AUTH_TOKEN = ''
    PEAK_COURSE_NAME = 'Kronbars Running'

    def find_free_places(self) -> str | None:
        free_place_info = self._get_places_info()

        if free_place_info is None:
            raise ValueError(f"PEAK_COURSE_NAME={self.PEAK_COURSE_NAME} not found")

        message_info = f"Available: {free_place_info.available}/{free_place_info.limit} places"
        logging.info(message_info)

        if free_place_info.available == 0:
            return None

        return message_info

    def _get_places_info(self) -> CourseInfo | None:
        for special_course in self._get_special_projects():
            if special_course.name != self.PEAK_COURSE_NAME:
                continue
            return special_course
        return None

    def _get_special_projects(self) -> list[CourseInfo]:
        headers = {
            "Authorization": f"Bearer {self.AUTH_TOKEN}"
        }
        resp = requests.get("https://my.itmo.ru/api/sport/my_sport/spec_projects", headers=headers)
        if resp.status_code > 200:
            raise ConnectionError("Auth error. Probably invalid auth token.")

        return [CourseInfo(**special_course) for special_course in resp.json()["result"]]

    def refresh_access_token_without_secret(
            self, refresh_token: str, client_id: str, token_url: str, realm: str
    ) -> None:
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
        }

        response = requests.post(f'{token_url}/realms/{realm}/protocol/openid-connect/token', data=data)

        if response.status_code == 200:
            new_access_token = response.json().get('access_token')
            self.AUTH_TOKEN = new_access_token
        else:
            raise ValueError(f"Ошибка при обновлении access token: {response.status_code}, {response.text}")
