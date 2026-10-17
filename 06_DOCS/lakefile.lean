import Lake
open Lake DSL

package tam20 {
  leanOptions := #[⟨`autoImplicit, false⟩]
}

@[default_target]
lean_lib TAM20 {
  srcDir := "."
}
