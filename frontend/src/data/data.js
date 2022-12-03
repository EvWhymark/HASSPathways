import pathwayCategoriesJSON from './json/pathway_categories.json'
import minor_categories_json from './json/minor_categories.json'
import yearsJSON from './json/years.json'

// Neatify JSON data:
// Sort pathways in pathway categories
pathwayCategoriesJSON.forEach(category => category.pathways.sort());
//Sort minor categories
minor_categories_json.forEach(minor=>minor.minors.sort())

// Prevent accidental modification
Object.freeze(yearsJSON);
Object.freeze(pathwayCategoriesJSON);
Object.freeze(minor_categories_json);

export const pathwayCategories = pathwayCategoriesJSON;
export const years = yearsJSON;
export const minor_categories=minor_categories_json;
