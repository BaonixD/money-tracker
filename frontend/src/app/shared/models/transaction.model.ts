export interface Transaction {
  id: number;
  amount: number;
  description: string | null;
  type: 'income' | 'expense';
  category_id: number;
  user_id: number;
  created_at: string;
}

export interface TransactionCreate {
  amount: number;
  description?: string;
  type: 'income' | 'expense';
  category_id: number;
}

export interface PaginatedResponse {
  items: Transaction[];
  total: number;
  limit: number;
  offset: number;
}

export interface StatisticsResponse {
  total_income: number;
  total_expense: number;
  balance: number;
}
