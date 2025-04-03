import {
  Select as SelectShadCN,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectGroup,
  SelectItem,
} from "./ui/select";

interface SelectProps {
  options: { label: string; value: string }[];
  onChange?: (value: string) => void;
  placeholder?: string;
}

const Select = ({ options, onChange, placeholder = "select" }: SelectProps) => {
  return (
    <SelectShadCN onValueChange={onChange}>
      <SelectTrigger
        data-cy="select-toggle"
        className="border-2 rounded-full  h-10 border-gray-500 focus:ring-2 focus:ring-gray-200 focus:border-gray-400 shadow-none bg-white text-muted-foreground"
      >
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent data-cy="select-menu" className="bg-white">
        <SelectGroup>
          {options.map(({ value, label }, index) => (
            <SelectItem key={index} value={value}>
              {label}
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </SelectShadCN>
  );
};

export default Select;
