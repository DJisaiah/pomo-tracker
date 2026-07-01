import flet as ft


class ImagePicker(ft.GridView):
    def __init__(
        self,
        filenames: iter,
        pre_path: str = "",
        **kwargs
    ):
        super().__init__(
            controls=self._get_images(
                filenames,
                pre_path
            ),
            scroll=ft.ScrollMode.ALWAYS,
            **kwargs
        )
        self._selected_filename: str = None
        self._pre_path_len = len(pre_path)
        #self.width=300,
        #self.height=200,
        #self.runs_count=3,
        #self.spacing=8,

    def get_selected_image_filename(self) -> None:
        return self._selected_filename

    def _image_on_hover(self, e: ft.ControlEvent) -> None:
        if e.control.data:
            return
        e.control.border = ft.Border.all(
            width=3,
            color=ft.Colors.GREEN_200
        ) if e.data else None

    def _image_on_click(self, e: ft.ControlEvent) -> None:
        # 1 to represent having been clicked 
        e.control.data = 1
        self._selected_filename = e.control.content.src[self._pre_path_len+1:]

        for control in e.control.parent.controls:
            if control is e.control:
                continue
            control.border = None
            control.data = None

    def _get_images(self,
        iterable: iter,
        pre_path: str = ""
    ) -> list[ft.Image]:
        images = []
        for filename in iterable:
            image = ft.Image(
                src=f"{pre_path}/{filename}"
            )

            image_container = ft.Container(
                content=image,
                on_hover=self._image_on_hover,
                on_click=self._image_on_click,
                bgcolor=ft.Colors.WHITE_10
            )
            
            
            images.append(image_container)
        return images
