import { LoaderIcon } from "lucide-react";
import {
  AlertDialog,
  AlertDialogTitle,
  AlertDialogContent,
  AlertDialogCancel,
  AlertDialogDescription,
  AlertDialogHeader,
  AlertDialogAction,
  AlertDialogFooter,
} from "@/components/ui/alert-dialog";
import { Input } from "./ui/input";
import { Button } from "./ui/button";

const QUESTIONS = [
  {
    question: "What is the name of the repository?",
    title: "Repository Name",
    type: "input",
    key: "name",
  },
  {
    question: "What is the name of the Organization?",
    title: "Organization Name",
    type: "input",
    key: "organization",
  },
];

type AddProps = {
  popup: {
    visible: boolean;
    title: string;
    name?: string;
    organization?: string;
    isValidating: boolean;
    isValid: boolean;
    message: string;
  };
  setPopup: (popup: AddProps["popup"]) => void;
  loading: boolean;
  onClick: () => void;
  validate: () => void;
};

const Add = ({ popup, setPopup, loading, onClick, validate }: AddProps) => {
  const handleInputChange = (key: string, value: string) => {
    setPopup({
      ...popup,
      [key]: value,
      isValidating: false,
      isValid: false,
      message: "",
    });
  };

  return (
    <AlertDialog open={popup.visible}>
      <AlertDialogContent className="flex flex-col">
        <AlertDialogHeader>
          <AlertDialogTitle>{popup.title || "Add Repository"}</AlertDialogTitle>
          <AlertDialogDescription>
            Please enter repository details and validate before adding.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <div className="flex flex-col gap-4 py-2">
          {QUESTIONS.map((question, index) => (
            <div key={index} className="flex flex-col gap-2">
              <label className="font-medium text-gray-700">
                {question.title}
              </label>
              {question.type === "input" && (
                <Input
                  type="text"
                  value={
                    (popup[question.key as keyof typeof popup] as string) || ""
                  }
                  onChange={(e) =>
                    handleInputChange(question.key, e.target.value)
                  }
                  placeholder={question.question}
                  className="border-gray-300"
                />
              )}
            </div>
          ))}
          <Button
            onClick={validate}
            disabled={popup.isValidating || !popup.name || !popup.organization}
            className="mt-2 bg-blue-100 text-blue-700 hover:bg-blue-200"
          >
            {popup.isValidating ? "Validating..." : "Validate Repository"}
          </Button>
          {popup.message && (
            <div
              className={`p-3 rounded-md text-sm ${
                popup.isValid
                  ? "bg-green-50 text-green-700 border border-green-200"
                  : "bg-red-50 text-red-700 border border-red-200"
              }`}
            >
              {popup.message}
            </div>
          )}
        </div>
        <AlertDialogFooter className="flex justify-end gap-2 mt-4">
          <AlertDialogCancel
            onClick={() => setPopup({ ...popup, visible: false })}
          >
            Cancel
          </AlertDialogCancel>
          <AlertDialogAction asChild>
            <Button
              onClick={onClick}
              disabled={!popup.isValid}
              className={
                popup.isValid
                  ? "bg-blue-600 text-white hover:bg-blue-700"
                  : "bg-gray-300 text-gray-500 cursor-not-allowed"
              }
            >
              {loading ? (
                <LoaderIcon className="animate-spin" />
              ) : (
                "Add Repository"
              )}
            </Button>
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
};

export default Add;
