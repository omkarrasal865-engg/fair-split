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

export interface CompletedSplitData {
  per_person: PersonResult[];
  grand_total: number;
  reconciliation: Reconciliation;
  paid_by: string | null;
  settle_up: Settlement[];
  assumptions: string[];
  flags: string[];
}

export interface ClarificationQuestion {
  id: string;
  type: string;
  item: string;
  remaining_quantity: number;
  remaining_amount: number;
  question: string;
}

export interface ClarificationResponse {
  questions: ClarificationQuestion[];
}

export interface SplitResult {
  status: "completed" | "needs_clarification";

  data: CompletedSplitData | null;

  clarification: ClarificationResponse | null;
}

export interface SplitBillResponse {
  success: boolean;

  request_id: string;

  data: SplitResult;
}