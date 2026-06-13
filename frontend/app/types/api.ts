export interface PersonResult {
  name: string;
  items: string[];
  subtotal: number;
  tax_share: number;
  service_share: number;
  discount_share: number;
  total: number;
}

export interface Settlement {
  from_person: string;
  to_person: string;
  amount: number;
}

export interface Reconciliation {
  sum_of_person_totals: number;
  grand_total: number;
  difference: number;
  matches_bill: boolean;
}

export interface SplitBillResponse {
  success: boolean;
  request_id: string;
  data: {
    per_person: PersonResult[];
    grand_total: number;
    reconciliation: Reconciliation;
    paid_by: string;
    settle_up: Settlement[];
    assumptions: string[];
    flags: string[];
    unallocated_items: string[];
  };
}