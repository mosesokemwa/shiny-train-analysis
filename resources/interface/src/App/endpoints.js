const version = '';

export default {
    JOBS: [version, "jobs"].join("/"),
    TAGS: [version, "tags"].join("/"),
    PROVIDERS: [version, "providers"].join("/"),
    SYNC: [version, "server-sync-jobs"].join("/"),
    CITIES: [version, "locations"].join("/"),

    API_AUTH_GOOGLE: [version, "auth" , "google", "login"].join("/"),
    API_AUTH_CANVAS: [version, "auth", "canvas", "login"].join("/"),
    API_AUTH_LOGOUT: [version, "auth", "logout"].join("/"),
    API_AUTH_CHECK: [version, "user"].join("/"),
}
