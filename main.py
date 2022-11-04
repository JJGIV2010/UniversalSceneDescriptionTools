#from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

class USD_Discussion:
    def __init__(self):
        self.git_url = "https://jjgiv2010.github.io/pxrd.github.io/"
        #self.stage = omni.usd.get_context().get_stage()

        self.variant_dict = {
            "name":"",
            "variant_sets":[],
            "variants":[],
            "variant_custom_attributes":[],
            "variant_transforms":[],
            "variant_rotations":[],
            "variant_scales":[],
            "variant_pivots":[]
        }

    def add_variant_set(self,variant_set):
        self.variant_dict['variant_sets'].append(variant_set)

    def add_variant(self,variant_set,variant_name):
        self.variant_dict['variants'].append((variant_set,variant_name))

    def create_new_nested_object(self,name,variant_sets,variants):
        self.variant_dict['name'] = name
        self.variant_dict['variant_sets'].append(variant_sets)
        self.variant_dict['variants'].append(variants)

    # def build_nested_object(self):
    #     self.main_xform = UsdGeom.Xform.Define(self.stage, f"/{self.variant_dict['name']}")
    #     self.main_prim = self.stage.DefinePrim(f"/{self.variant_dict['name']}/{self.variant_dict['name']}_Variants")
    #
    #     for i in range(len(self.variant_dict['variant_sets'])):
    #         variant_set = self.main_prim.GetVariantSets().AddVariantSet(self.variant_dict['variant_sets'][i])
    #
    #         if self.variant_dict['variants'][i][0] == self.variant_dict['variant_sets'][i]:
    #             variant_set.AddVariant(self.variant_dict['variants'][i][1])
    #             variant_set.SetVariantSelection(self.variant_dict['variants'][i][1])
    #
    #             with variant_set.GetVariantEditContext():
    #                 new_variant_prim_path = self.stage.DefinePrim(self.main_prim.GetPath().AppendChild(
    #                     f"{self.variant_dict['variants'][i][1]}_mesh"))
    #                 new_variant_prim_path.GetReferences().AddReference(
    #                     f"{self.git_url}/{self.variant_dict['name']}/{self.variant_dict['variant_sets'][i]}/{self.variant_dict['variants'][i][0]}.usda")
    #         else:
    #             pass

object_builder = USD_Discussion()
object_builder.create_new_nested_object(
    "food",
    ["burritos","tacos"],
    [
        ("burritos","chicken"),
        ("burritos","fish"),
        ("burritos","carnitas"),
        ("tacos", "steak"),
        ("tacos", "chicken")

    ]

)
