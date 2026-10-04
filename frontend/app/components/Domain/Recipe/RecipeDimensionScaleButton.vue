<template>
  <div v-if="dimensionDisplay">
    <v-menu
      v-model="menu"
      :disabled="!canEditScale"
      offset-y
      top
      nudge-top="6"
      :close-on-content-click="false"
    >
      <template #activator="{ props: activatorProps }">
        <v-tooltip
          v-if="canEditScale"
          size="small"
          location="top"
          color="secondary-darken-1"
        >
          <template #activator="{ props: tooltipProps }">
            <v-card
              class="pa-1 px-2"
              dark
              color="secondary-darken-1"
              size="small"
              v-bind="{ ...activatorProps, ...tooltipProps }"
            >
              <v-icon size="small" class="mr-2">
                {{ $globals.icons.edit }}
              </v-icon>
              <span>{{ dimensionDisplay }}</span>
            </v-card>
          </template>
          <span>{{ $t("recipe.edit-scale") }}</span>
        </v-tooltip>
        <v-card
          v-else
          class="pa-1 px-2"
          dark
          color="secondary-darken-1"
          size="small"
          v-bind="activatorProps"
        >
          <span>{{ dimensionDisplay }}</span>
        </v-card>
      </template>
      <v-card min-width="320px">
        <v-card-title>{{ $t("recipe.target-size") }}</v-card-title>
        <v-card-text>
          <div class="d-flex align-center ga-3">
            <v-number-input
              :model-value="targetLength"
              :min="0"
              :precision="null"
              :label="primaryDimensionLabel"
              :suffix="unit"
              variant="underlined"
              control-variant="hidden"
              @update:model-value="updateTargetLength"
            />
            <v-number-input
              v-if="basis === 'rectangle'"
              :model-value="targetWidth"
              :min="0"
              :precision="null"
              :label="$t('recipe.width')"
              :suffix="unit"
              variant="underlined"
              control-variant="hidden"
              @update:model-value="updateTargetWidth"
            />
            <v-tooltip location="end" color="secondary-darken-1">
              <template #activator="{ props: resetTooltipProps }">
                <v-btn
                  v-bind="resetTooltipProps"
                  icon
                  flat
                  size="small"
                  @click="resetScale"
                >
                  <v-icon>{{ $globals.icons.undo }}</v-icon>
                </v-btn>
              </template>
              <span>{{ $t("recipe.reset-scale") }}</span>
            </v-tooltip>
          </div>
        </v-card-text>
      </v-card>
    </v-menu>
  </div>
</template>

<script setup lang="ts">
import { calculateRecipeDimensionScale } from "~/composables/recipes/use-recipe-dimension-scaling";
import type { RecipeScaleBasis, RecipeScaleUnit } from "~/lib/api/types/recipe";

interface Props {
  basis: RecipeScaleBasis;
  unit: RecipeScaleUnit;
  baseLength: number;
  baseWidth?: number;
  editScale?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  baseWidth: 0,
  editScale: false,
});

const scale = defineModel<number>({ required: true });
const i18n = useI18n();
const menu = ref(false);
const targetLength = ref(props.baseLength);
const targetWidth = ref(props.baseWidth);

const hasValidBase = computed(() =>
  props.baseLength > 0
  && (props.basis !== "rectangle" || props.baseWidth > 0),
);
const canEditScale = computed(() => props.editScale && hasValidBase.value);

const primaryDimensionLabel = computed(() => {
  if (props.basis === "round") {
    return i18n.t("recipe.diameter");
  }
  if (props.basis === "square") {
    return i18n.t("recipe.side-length");
  }
  return i18n.t("recipe.length");
});

function formatDimension(value: number): string {
  return Number(value.toFixed(3)).toString();
}

const dimensionDisplay = computed(() => {
  if (!hasValidBase.value) {
    return "";
  }

  const length = formatDimension(targetLength.value);
  if (props.basis === "round") {
    return i18n.t("recipe.round-size", { diameter: length, unit: props.unit });
  }
  if (props.basis === "square") {
    return i18n.t("recipe.square-size", { length, unit: props.unit });
  }
  return i18n.t("recipe.rectangle-size", {
    length,
    width: formatDimension(targetWidth.value),
    unit: props.unit,
  });
});

function recalculateScale() {
  scale.value = calculateRecipeDimensionScale({
    basis: props.basis,
    baseLength: props.baseLength,
    baseWidth: props.baseWidth,
    targetLength: targetLength.value,
    targetWidth: targetWidth.value,
  });
}

function updateTargetLength(value: number | null) {
  if (value === null || value <= 0) {
    return;
  }
  targetLength.value = value;
  recalculateScale();
}

function updateTargetWidth(value: number | null) {
  if (value === null || value <= 0) {
    return;
  }
  targetWidth.value = value;
  recalculateScale();
}

function resetScale() {
  targetLength.value = props.baseLength;
  targetWidth.value = props.baseWidth;
  scale.value = 1;
}

watch(
  () => [props.basis, props.baseLength, props.baseWidth, props.unit],
  resetScale,
);
</script>
