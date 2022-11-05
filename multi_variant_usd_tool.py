from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

class USD_VariantTool:
    def __init__(self):
        self.main_directory_or_url = ""
        self.stage = omni.usd.get_context().get_stage()
        self.variant_dict = {
            "name":"",
            "variant_sets":[],
            "variants":[],
            "variant_custom_attributes":[]
        }
        self.sdf_dict = {
            int: Sdf.ValueTypeNames.Int,
            float: Sdf.ValueTypeNames.Float,
            str: Sdf.ValueTypeNames.String
        }

    def add_comment(self,prim_path,text):
        prim = self.stage.GetPrimAtPath(prim_path)
        prim.SetMetadata('comment',text)

    def set_kind(self,path,kind):
        omni.kit.commands.execute('ChangeMetadata',
                                  object_paths=[Sdf.Path(path)],
                                  key='kind',
                                  value=kind)

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

    def build_new_nested_object(self):
        self.main_xform = UsdGeom.Xform.Define(self.stage, f"/{self.variant_dict['name']}")
        self.main_prim = self.stage.DefinePrim(f"/{self.variant_dict['name']}/{self.variant_dict['name']}_Variants")

        self.set_kind(self.main_xform.GetPath().pathString,"assembly")
        self.add_comment(self.main_xform.GetPath().pathString,
                         f"Main {self.variant_dict['name']} assembly, with {len(self.variant_dict['variant_sets'])} variant sets ")

        self.set_kind(self.main_prim.GetPath().pathString, "group")
        self.add_comment(self.main_prim.GetPath().pathString,
                         f"{self.variant_dict['name']} group, with {len(self.variant_dict['variants'])} components as variants ")

        for i in range(len(object_builder.variant_dict['variant_sets'])):
            for k in range(len(object_builder.variant_dict['variants'])):
                variant_set = self.main_prim.GetVariantSets().AddVariantSet(self.variant_dict['variant_sets'][i])

                if self.variant_dict['variants'][k][0] == self.variant_dict['variant_sets'][i]:
                    variant_set.AddVariant(self.variant_dict['variants'][k][1])
                    variant_set.SetVariantSelection(self.variant_dict["variants"][k][1])

                    with variant_set.GetVariantEditContext():
                        new_variant_prim = self.stage.DefinePrim(self.main_prim.GetPath().AppendChild(
                            f"{self.variant_dict['variants'][k][1]}_mesh"))
                        self.set_kind(new_variant_prim.GetPath().pathString, "component")
                        self.add_comment(new_variant_prim.GetPath().pathString,
                                         f"{self.variant_dict['variants'][k][1]} component custom attributes ")

                        new_variant_prim.GetReferences().AddReference(
                           f"{self.main_directory_or_url}/{self.variant_dict['name']}/{self.variant_dict['variant_sets'][i]}/{self.variant_dict['variants'][i][0]}.usda")
                        for a in range(len(self.variant_dict['variant_custom_attributes'])):
                            if self.variant_dict['variant_custom_attributes'][a][0] == self.variant_dict['variant_sets'][i]:
                                if self.variant_dict['variant_custom_attributes'][a][1] == self.variant_dict['variants'][k][1]:
                                    new_attribute = new_variant_prim.CreateAttribute(
                                        self.variant_dict['variant_custom_attributes'][a][2],
                                        self.sdf_dict[type(self.variant_dict['variant_custom_attributes'][a][3])])
                                    new_attribute.Set(self.variant_dict['variant_custom_attributes'][a][3])

                else:
                    pass

    def _show_as_string(self):
        print(self.stage.GetRootLayer().ExportToString())

object_builder = USD_VariantTool()

object_builder.create_new_nested_object("food",["burritos","tacos"],[
        ("burritos","chicken"),
        ("burritos","fish"),
        ("burritos","carnitas"),
        ("tacos", "steak"),
        ("tacos", "chicken")
    ],[
        ("burritos", "chicken","test_int",10),
        ("burritos", "fish","test_float",2.0),
        ("burritos", "carnitas","sauce","light"),
        ("tacos", "steak","sauce","none"),
        ("tacos", "chicken","sauce","super spicy")
    ])

object_builder.build_new_nested_object()
