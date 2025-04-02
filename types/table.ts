export type Filters = {
  id: string;
  value: unknown;
};

export type Document = {
  id: string;
  title: string;
  user: string;
  created_at: string;
  mergable: boolean;
};
