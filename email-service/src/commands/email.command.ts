export interface EmailCommand {
    to: string[];
    from: string;
    subject: string;
    body:string;
    isHtml: boolean;
    cc?: string[]|null;
    category: string;
    attachments?: string[]|null;
}

export enum EmailCommandCategory {
    GENERAL = 'general',
    TECHNICAL = 'technical',
    BILLING = 'billing',
}