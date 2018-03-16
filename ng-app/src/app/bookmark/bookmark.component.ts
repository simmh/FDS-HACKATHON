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
    public image: string,
    public favicon: string
  ) {}
}

@Component({
  selector: 'app-bookmark',
  templateUrl: './bookmark.component.html',
  styleUrls: ['./bookmark.component.css']
})

export class BookmarkComponent implements OnInit {
  bookamrks: [''];
  title: 'BOOKMARK';
  bookmarksDB: Bookmark[];
  bookmarks: any;
  summary: Summary;

  checkStatus = false;
  toggleStar = false;
  toggleTrash = false;

  checkList = [];

  url_summary = 'http://localhost:8000';



  key = 'key';

  // HttpClient를 컴포넌트에 주입
  constructor(public http: HttpClient) { }

  generateId() {
    return this.bookmarks.length ? Math.max.apply(null, this.bookmarks.map(function (item) {
      return item.id;
    })) + 1 : 1;
  }

  getBookmarks() {
    console.log(['GET bookmakrs', this.bookmarksDB]);
    this.bookmarks = this.bookmarksDB;
  }

  getSummary(url) {
    console.log('[GET SUMMARY]')
    const host = 'http://localhost:8000/summary?url=';
    this.http.get(host + url, { observe: 'response' })
      // 요청 결과를 프로퍼티에 할당
      .subscribe(data => {
        this.summary = data.body;
        // this.bookmarks = data.body;
        console.log('summary', data);
      } ,(err: HttpErrorResponse) => {
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

  bookmarkAdd(url) {
    console.log('[GET SUMMARY & ADD]', url);
    if (!url) { return; }
    const host = 'http://localhost:8000/summary?url=';

    this.http.get<Bookmark[]>(host + url, { observe: 'response' })
      // 요청 결과를 프로퍼티에 할당
      .subscribe(data => {
        console.log('bookmarkAdd data', data.body);
        const item = Object.assign({}, data.body, { id: this.generateId()} );
        this.bookmarksDB = [item, ...this.bookmarks];
        this.getBookmarks();
        this.inputURL.value= '';
        // this.summary = this.Summary;
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


  searchBookmark(keyword) {
    console.log('[ Search bookmark]', keyword);
    console.log('[ Search bookmarkDB]', this.bookmarksDB);
    console.log('[ Search bookmark list]', this.bookmarks);
    // this.bookamrks = this.bookmarksDB.filter(function (item) {
    //   return (item.title.match(keyword) || item.description.match(keyword));
    // });
    this.bookmarks = this.bookmarksDB.filter(function (item) {
      return (item.title.match(keyword) || item.description.match(keyword));
      });
  }

  getStarBookmark() {
    console.log('[GET star bookmark]');
    if (this.toggleStar) {
      this.bookmarks = this.bookmarksDB.filter(function (item) {
        return item.star;
      });
    } else {
      this.getBookmarks();
    }
    this.toggleStar = !this.toggleStar;
  }

  setStarBookmark(id: number) {
    console.log('[SET star bookmark]', id);
    this.bookmarksDB = this.bookmarks.map(function (item) {
      if (item.id === id) { item.star = !item.star; }
      return item;
    });
    this.getBookmarks();
  }

  bookmarkDelete(id: number) {
    console.log('[DELETE bookmarkDelete()]', id);
    this.bookmarksDB = this.bookmarks.filter(function (item) {
      return item.id !== id;
    });
    this.getBookmarks();
  }

  checkCard(id: number) {
    const checkList = this.checkList;

    const checkIndex = checkList.indexOf(id);
    if  ( checkIndex < 0 ) {
      // 추가
      this.checkList = [...checkList, id];
    } else {
      this.checkList = checkList.filter(function(item, index){
        return item !== id;
      });
    }
    console.log('[Check id]', id);
    console.log('[Check list]', this.checkList);
    console.log('[Check list is id  index??]', (checkIndex));
  }

  setBookmarks() {
    const url = 'http://localhost:8000/bookmarks/'
    this.http.get<Bookmark[]>(url)
      // 요청 결과를 프로퍼티에 할당
      .subscribe(bookmark => {
        this.bookmarksDB = bookmark;
        this.bookmarks = bookmark;

        console.log(bookmark);
      });
  } 

  ngOnInit() {
    this.setBookmarks();
  }
}



