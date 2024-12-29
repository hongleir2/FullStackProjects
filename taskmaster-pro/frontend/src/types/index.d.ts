interface User {
    id: number;
    email: string;
}

interface Task {
    id: number;
    title: string;
    description?: string;
    due_date?: string;
    is_completed: boolean;
    owner_id: number;
}

interface AppState {
    loading: boolean;
    error: string | null;
    user: User | null;
    tasks: Task[];
    setUser: (user: User | null) => void;
    setTasks: (tasks: Task[]) => void;
    addTask: (task: Task) => void;
    updateTask: (task: Task) => void;
    deleteTask: (taskId: number) => void;
}

export { User, Task, AppState };