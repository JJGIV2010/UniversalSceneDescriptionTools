from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

class OV_USD_Tools:
    def __init__(self):
        self.stage = omni.usd.get_context().get_stage()
        self.xform_transforms_list = []
        self.xform_rotations_list = []
        self.xform_scales_list = []
        self.xform_pivots_list = []

        self.json_output = {}

    def create_xforms(self):
        pass

    def get_all_xform_transforms(self):
        pass

    def get_all_xform_rotations(self):
        pass

    def get_all_xform_scales(self):
        pass

    def get_all_xform_pivots(self):
        pass

    def create_json_output(self):
        pass

    def get_json_output(self):
        return self.json_output
    
