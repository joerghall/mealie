<template>
  <div class="d-flex align-center ga-2 pt-2 pb-3">
    <RecipeUnitSystemButton
      v-if="!isEditMode"
      :recipe="recipe"
    />
    <RecipeScaleEditButton
      v-if="!isEditMode && scaleBasis === 'servings'"
      v-model.number="scale"
      :recipe-servings="recipeServings"
      :edit-scale="hasFoodOrUnit && !isEditMode"
    />
    <RecipeDimensionScaleButton
      v-else-if="!isEditMode"
      v-model.number="scale"
      :basis="scaleBasis"
      :unit="recipe.recipeScaleUnit"
      :base-length="recipe.recipeScaleBaseLength"
      :base-width="recipe.recipeScaleBaseWidth"
      :edit-scale="hasFoodOrUnit && !isEditMode"
    />
  </div>
</template>

<script setup lang="ts">
import RecipeScaleEditButton from "~/components/Domain/Recipe/RecipeScaleEditButton.vue";
import RecipeDimensionScaleButton from "~/components/Domain/Recipe/RecipeDimensionScaleButton.vue";
import RecipeUnitSystemButton from "~/components/Domain/Recipe/RecipeUnitSystemButton.vue";
import type { NoUndefinedField } from "~/lib/api/types/non-generated";
import type { Recipe, RecipeScaleBasis } from "~/lib/api/types/recipe";
import { usePageState } from "~/composables/recipe-page/shared-state";

const props = defineProps<{ recipe: NoUndefinedField<Recipe> }>();

const scale = defineModel<number>({ default: 1 });

const { isEditMode } = usePageState(props.recipe.slug);

const recipeServings = computed<number>(() => {
  return props.recipe.recipeServings || props.recipe.recipeYieldQuantity || 1;
});

const scaleBasis = computed<RecipeScaleBasis>(() => {
  return props.recipe.recipeScaleBasis || "servings";
});

const hasFoodOrUnit = computed(() => {
  if (props.recipe.recipeIngredient) {
    for (const ingredient of props.recipe.recipeIngredient) {
      if (ingredient.food || ingredient.unit) {
        return true;
      }
    }
  }
  return false;
});
</script>
