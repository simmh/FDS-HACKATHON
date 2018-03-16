import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

class Bookmark {
  constructor(
    public id: number,
    public url: string,
    public domain: string,
    public title: string,
    public description: string,
    public favicon: string,
    public image: string,
    public star: boolean,
  ) {}
}

class Summary {
  constructor(
    public url: string,
    public domin: string,
    public title: string,
    public description: string,
    public iamge: string,
    public favicon: string
  ) {}
}

@Component({
  selector: 'app-bookmark',
  templateUrl: './bookmark.component.html',
  styleUrls: ['./bookmark.component.css']
})

export class BookmarkComponent implements OnInit {
  title: 'BOOKMARK';
  bookmarks: Bookmark[];
  summary: Summary;


  // host = 'http://localhost:8000';
  host = 'http://192.168.0.53:8000';


  url = this.host + '/bookmarks/';
  url_star = this.host + '/bookmarks/star/';
  url_set_star = this.host + '/bookmark/star/';
  url_search = this.host + '/bookmarks/search/';
  
  url_summary = this.host + '/summary?url=';
  url_create = this.host + '/bookmark/create?url=';
  url_delete = this.host + '/bookmark/delete/';

  key = 'key';

  // HttpClient를 컴포넌트에 주입
  constructor(public http: HttpClient) { }

  

  getBookmarks() {
    this.http.get<Bookmark[]>(this.url)
      // 요청 결과를 프로퍼티에 할당
      .subscribe(bookmark => {
        this.bookmarks = bookmark;
        console.log(bookmark);
      });
  }

  getSummary(url) {
    console.log('[GET SUMMARY]')
    this.http.get(this.url_summary + url, { observe: 'response' })
      // 요청 결과를 프로퍼티에 할당
      .subscribe(data => {
        this.summary = data;
        console.log(data);
        console.log(data.status);
      }, (err: HttpErrorResponse) => {
        // this.summary = Summary;
        this.summary = 'Not found';
        if (err.error instanceof Error) {
          // 클라이언트 또는 네트워크 에러
          console.log(`Client-side error: ${err.error.message}`);
        } else {
          // 백엔드가 실패 상태 코드 응답
          console.log(`Server-side error: ${err.status}`);
        }
      });
  }
  getStarBookmark() {
    console.log('[GET star bookmark]');

    this.http.get<Bookmark[]>(this.url_star)
      // 요청 결과를 프로퍼티에 할당
      .subscribe(bookmark => {
        this.bookmarks = bookmark;
        console.log(bookmark);
      });
  }

  searchBookmark(keyword) {
    console.log('[SET star bookmark]', keyword);
    this.http.get<Bookmark[]>(this.url_search + keyword)
      // 요청 결과를 프로퍼티에 할당
      .subscribe(bookmark => {
        this.bookmarks = bookmark;
        console.log(bookmark);
      });
  }

  setStarBookmark(id) {
    console.log('[SET star bookmark]');
    this.http.get(this.url_set_star + id)
      // 요청 결과를 프로퍼티에 할당
      .subscribe(bookmark => {
        this.getBookmarks();
      });
  }

  bookmarkAdd(url) {
    console.log('[input url add]', url);

    this.http.get(this.url_create + url)
      // 요청 결과를 프로퍼티에 할당
      .subscribe(data => {
        console.log(data);
        this.getBookmarks();
      });
  }

  bookmarkDelete(id) {
    console.log('[DELETE bookmarkDelete()]', id);
    this.http.get(this.url_delete + id)
      // 요청 결과를 프로퍼티에 할당
      .subscribe(data => {
        // this.bookmarks = bookmark;
        console.log(data);
        this.getBookmarks();
      }

    );
  }

  ngOnInit() {
    this.getBookmarks();
  }
}



