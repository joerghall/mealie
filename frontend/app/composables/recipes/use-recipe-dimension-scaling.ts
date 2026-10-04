import type { RecipeScaleBasis } from "~/lib/api/types/recipe";

interface RecipeDimensionScale {
  basis: RecipeScaleBasis;
  baseLength: number;
  baseWidth?: number;
  targetLength: number;
  targetWidth?: number;
}

export function calculateRecipeDimensionScale({
  basis,
  baseLength,
  baseWidth = 0,
  targetLength,
  targetWidth = 0,
}: RecipeDimensionScale): number {
  if (basis === "servings" || baseLength <= 0 || targetLength <= 0) {
    return 1;
  }

  if (basis === "rectangle") {
    if (baseWidth <= 0 || targetWidth <= 0) {
      return 1;
    }

    return (targetLength * targetWidth) / (baseLength * baseWidth);
  }

  return (targetLength / baseLength) ** 2;
}
