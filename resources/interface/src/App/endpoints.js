const version = 'api';

export default {
    JOBS: [version, "jobs"].join("/"),
    TAGS: [version, "tags"].join("/"),
    PROVIDERS: [version, "providers"].join("/"),
    SYNC: [version, "server-sync-jobs"].join("/"),
    CITIES: [version, "locations"].join("/"),

    API_AUTH_GOOGLE: ["auth" , "google", "login"].join("/"),
    API_AUTH_CANVAS: ["auth", "canvas", "login"].join("/"),
    API_AUTH_LOGOUT: ["auth", "logout"].join("/"),
    API_AUTH_CHECK: [version, "user"].join("/"),
}
