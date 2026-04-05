import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Category, CategoryCreate } from '../shared/models/category.model';
import {
  Transaction,
  TransactionCreate,
  PaginatedResponse,
  StatisticsResponse,
} from '../shared/models/transaction.model';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  // Categories
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.baseUrl}/categories/`);
  }

  createCategory(data: CategoryCreate): Observable<Category> {
    return this.http.post<Category>(`${this.baseUrl}/categories/create`, data);
  }

  deleteCategory(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/categories/${id}`);
  }

  // Transactions
  getTransactions(params?: {
    category_id?: number;
    type?: string;
    date_from?: string;
    date_to?: string;
    limit?: number;
    offset?: number;
  }): Observable<PaginatedResponse> {
    let httpParams = new HttpParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          httpParams = httpParams.set(key, value.toString());
        }
      });
    }
    return this.http.get<PaginatedResponse>(`${this.baseUrl}/transactions/`, {
      params: httpParams,
    });
  }

  createTransaction(data: TransactionCreate): Observable<Transaction> {
    return this.http.post<Transaction>(
      `${this.baseUrl}/transactions/create`,
      data
    );
  }

  deleteTransaction(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/transactions/${id}`);
  }

  // Statistics
  getStatistics(dateFrom?: string, dateTo?: string): Observable<StatisticsResponse> {
    let params = new HttpParams();
    if (dateFrom) params = params.set('date_from', dateFrom);
    if (dateTo) params = params.set('date_to', dateTo);
    return this.http.get<StatisticsResponse>(
      `${this.baseUrl}/transactions/stats`,
      { params }
    );
  }
}
