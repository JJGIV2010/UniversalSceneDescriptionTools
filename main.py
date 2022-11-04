#from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

class USD_Discussion:
    def __init__(self):
        self.git_url = "https://jjgiv2010.github.io/pxrd.github.io/"
        #self.stage = omni.usd.get_context().get_stage()
        self.variant_dict = {
            "name":"",
            "variant_sets":[],
            "variants":[],
            "variant_custom_attributes":[]
        }

    def add_variant_set(self,variant_set):
        self.variant_dict['variant_sets'].append(variant_set)
    def add_variant(self,variant_set,variant_name):
        self.variant_dict['variants'].append((variant_set,variant_name))
    def add_custom_attribute(self,variant_set,variant,attribute_name,attribute_value):
        self.variant_dict['variant_custom_attributes'].append((variant_set,variant,attribute_name,attribute_value))

    def create_new_nested_object(self,name,variant_sets,variants,var_attributes):
        self.variant_dict['name'] = name
        for v_set in range(len(variant_sets)):
            self.add_variant_set(variant_sets[v_set])
        for i in range(len(variants)):
            self.add_variant(variants[i][0],variants[i][1])
        for i in range(len(var_attributes)):
            self.add_custom_attribute(var_attributes[i][0],var_attributes[i][1],var_attributes[i][2],var_attributes[i][3])

    # def build_new_nested_object(self):
    #     self.main_xform = UsdGeom.Xform.Define(self.stage, f"/{self.variant_dict['name']}")
    #     self.main_prim = self.stage.DefinePrim(f"/{self.variant_dict['name']}/{self.variant_dict['name']}_Variants")
    #
    #     for i in range(len(self.variant_dict["variant_sets"])):
    #         variant_set = self.main_prim.GetVariantSets().AddVariantSet(self.variant_dict["variant_sets"][i])
    #
    #         if self.variant_dict["variants"][i][0] == self.variant_dict["variant_sets"][i]:
    #             variant_set.AddVariant(self.variant_dict["variants"][i][1])
    #             variant_set.SetVariantSelection(self.variant_dict["variants"][i][1])
    #
    #             with variant_set.GetVariantEditContext():
    #                 new_variant_prim_path = self.stage.DefinePrim(self.main_prim.GetPath().AppendChild(
    #                     f"{self.variant_dict['variants'][i][1]}_mesh"))
    #                 #new_variant_prim_path.GetReferences().AddReference(
    #                  #   f"{self.git_url}/{self.variant_dict['name']}/{self.variant_dict['variant_sets'][i]}/{self.variant_dict['variants'][i][0]}.usda")
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

    ],
    [
        ("burritos", "chicken","sauce","hot"),
        ("burritos", "fish","sauce","mild"),
        ("burritos", "carnitas","sauce","light"),
        ("tacos", "steak","sauce","none"),
        ("tacos", "chicken","sauce","super spicy")
    ])
for i in range(len(object_builder.variant_dict['variant_sets'])):
    for k in range(len(object_builder.variant_dict['variants'])):
        if object_builder.variant_dict['variants'][k][0] == object_builder.variant_dict['variant_sets'][i]:
            print(f"match for variant_set: {object_builder.variant_dict['variant_sets'][i]} with {object_builder.variant_dict['variants'][k]}")
            print(object_builder.variant_dict['variants'][k][1])
#object_builder.build_new_nested_object()