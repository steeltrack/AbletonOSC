from functools import partial
from typing import Optional, Tuple, Any
from .handler import AbletonOSCHandler

class ViewHandler(AbletonOSCHandler):
    def __init__(self, manager):
        super().__init__(manager)
        self.class_identifier = "view"

    def init_api(self):
        def get_selected_scene(params: Optional[Tuple] = ()):
            return (list(self.song.scenes).index(self.song.view.selected_scene),)

        def get_selected_track(params: Optional[Tuple] = ()):
            return (list(self.song.tracks).index(self.song.view.selected_track),)
        
        def selected_track_changed(params: Optional[Tuple] = ()):
            self.logger.info("Property %s changed of %s %s: %s" % ('track', self.class_identifier, str(params), get_selected_track()))
            self.osc_server.send("/live/view/get/selected_track", get_selected_track())

        def get_selected_clip(params: Optional[Tuple] = ()):
            return (get_selected_track()[0], get_selected_scene()[0])

        def set_selected_scene(params: Optional[Tuple] = ()):
            self.song.view.selected_scene = self.song.scenes[params[0]]

        def set_selected_track(params: Optional[Tuple] = ()):
            self.song.view.selected_track = self.song.tracks[params[0]]

        def set_selected_clip(params: Optional[Tuple] = ()):
            set_selected_track((params[0],))
            set_selected_scene((params[1],))

        def set_selected_device(params: Optional[Tuple] = ()):
            device = self.song.tracks[params[0]].devices[params[1]]
            self.song.view.select_device(device)
            return params[0], params[1]

        self.osc_server.add_handler("/live/view/get/selected_scene", get_selected_scene)
        self.osc_server.add_handler("/live/view/get/selected_track", get_selected_track)
        self.song.view.add_selected_track_listener(selected_track_changed)
        self.osc_server.add_handler("/live/view/get/selected_clip", get_selected_clip)
        self.osc_server.add_handler("/live/view/set/selected_scene", set_selected_scene)
        self.osc_server.add_handler("/live/view/set/selected_track", set_selected_track)
        self.osc_server.add_handler("/live/view/set/selected_clip", set_selected_clip)
        self.osc_server.add_handler("/live/view/set/selected_device", set_selected_device)