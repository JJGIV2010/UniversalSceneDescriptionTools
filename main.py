from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

class USD_Discussion:
    def __init__(self):
        self.git_url = "https://jjgiv2010.github.io/pxrd.github.io/"
        self.stage = omni.usd.get_context().get_stage()

        self.object_main_name = "example_main"

        self.variant_sets = [
            "example_set_a",
            "example_set_b"
        ]

        self.variant_set_name_path = [
            ("example_set_a", "variant_a"),
            ("example_set_a", "variant_b"),
            ("example_set_b", "variant_a"),
            ("example_set_b", "variant_b")
        ]

    def build_nested_usd_object(self):
        self.main_xform = UsdGeom.Xform.Define(self.stage, f"/{self.object_main_name}")
        self.main_prim = self.stage.DefinePrim(f"/{self.object_main_name}/{self.object_main_name}_Variants")

        for i in range(len(self.variant_sets)):
            variant_set = self.main_prim.GetVariantSets().AddVariantSet(self.variant_sets[i])

            if self.variant_set_name_path[i][0] == self.variant_sets[i]:
                variant_set.AddVariant(self.variant_set_name_path[i][1])
                variant_set.SetVariantSelection(self.variant_set_name_path[i][1])

                with variant_set.GetVariantEditContext():
                    new_variant_prim_path = self.stage.DefinePrim(self.main_prim.GetPath().AppendChild(
                        f"{self.variant_set_name_path[i][1]}_mesh"))
                    new_variant_prim_path.GetReferences().AddReference(
                        f"{self.git_url}/{self.object_main_name}/{self.variant_sets[i]}/{self.variant_set_name_path[1]}.usda")
            else:
                pass
