from typing import Any, Iterable

import flet as ft


class ImagePicker(ft.GridView):
    def __init__(self, filenames: Iterable[str], pre_path: str = "", **kwargs: Any):
        super().__init__(
            controls=self._get_images(  # type: ignore
                filenames, pre_path
            ),
            scroll=ft.ScrollMode.ALWAYS,
            **kwargs,
        )
        self._selected_filename: str | None = None
        self._pre_path_len = len(pre_path)

    def get_selected_image_filename(self) -> str | None:
        return self._selected_filename

    def _image_on_hover(self, e: ft.ControlEvent) -> None:
        if e.control.data:
            return
        e.control.border = (  # type: ignore
            ft.Border.all(  # type: ignore
                width=3, color=ft.Colors.GREEN_200
            )
            if e.data
            else None
        )

    def _image_on_click(self, e: ft.ControlEvent) -> None:
        # True to represent having been clicked, False otherwise
        e.control.data = True

        # update current selected filename
        # when a control in the image gallery is clicked
        self._selected_filename = e.control.content.src[self._pre_path_len + 1 :]  # type: ignore

        for control in self.controls:
            if control is e.control:
                continue
            control.border = None  # type: ignore
            control.data = False

    def _get_images(
        self, iterable: Iterable[str], pre_path: str = ""
    ) -> list[ft.Image]:
        images = []
        for filename in iterable:
            image = ft.Image(src=f"{pre_path}/{filename}")

            image_container = ft.Container(
                content=image,
                on_hover=self._image_on_hover,  # type: ignore
                on_click=self._image_on_click,  # type: ignore
                bgcolor=ft.Colors.WHITE_10,
            )
            images.append(image_container)
        return images
