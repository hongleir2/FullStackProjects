import { create } from 'zustand';
import { User, Task, AppState } from './types';

// Create a store with the initial state and actions
const useStore = create<AppState>((set) => ({
    user: null,
    tasks: [],
    
    setUser: (user: User | null) => set({ user }),

    // Expain set(partial: PartialState<TState>, replace?: boolean): void; method
    // The set method is used to update the store state. It takes a partial state object as an argument and merges it with the current state.
    setTasks: (tasks: Task[]) => set({ tasks }),

    // Explain set(updater: (state: TState) => PartialState<TState>, replace?: boolean): void;
    // The set method can also take a function as an argument. 
    // The function receives the current state as an argument and should return a partial state object.
    addTask: (task: Task) =>
        set((state) => ({ tasks: [...state.tasks, task] })),

    updateTask: (updatedTask: Task) =>
        set((state) => ({
            tasks: state.tasks.map((task) =>
                task.id === updatedTask.id ? updatedTask : task
            ),
        })),

    deleteTask: (taskId: number) =>
        set((state) => ({
            tasks: state.tasks.filter((task) => task.id !== taskId),
        })),
}));


export default useStore;