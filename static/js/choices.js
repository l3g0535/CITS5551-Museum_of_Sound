var multi = new SelectPure(".select-tag", {
  options: [
    {
      label: "Nature",
      value: "Nature",
    },
    {
      label: "Beach",
      value: "Beach",
    },
    {
      label: "People",
      value: "People",
    },
    {
      label: "Hall",
      value: "Hall",
    },
    {
      label: "Animals",
      value: "Animals",
    },
    {
      label: "Urban",
      value: "Urban",
    },
  ],
  multiple: true,
  placeholder: "-Please select-",
  icon: "fa fa-times",
  onChange: (value) => {
    console.log(value);
  },
  classNames: {
    select: "select-pure__select",
    dropdownShown: "select-pure__select--opened",
    multiselect: "select-pure__select--multiple",
    label: "select-pure__label",
    placeholder: "select-pure__placeholder",
    dropdown: "select-pure__options",
    option: "select-pure__option",
    autocompleteInput: "select-pure__autocomplete",
    selectedLabel: "select-pure__selected-label",
    selectedOption: "select-pure__option--selected",
    placeholderHidden: "select-pure__placeholder--hidden",
    optionHidden: "select-pure__option--hidden",
  },
});
var resetMulti = function () {
  multi.reset();
};
